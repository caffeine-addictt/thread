import time
import pytest
from src.thread import Thread, exceptions


# >>>>>>>>>> Dummy Functions <<<<<<<<<< #
def _dummy_target_raiseToPower(x: float, power: float, delay: float = 0):
  time.sleep(delay)
  return x**power

def _dummy_raiseException(x: Exception, delay: float = 0):
  time.sleep(delay)
  raise x




# >>>>>>>>>> General Use <<<<<<<<<< #
def test_threadCreation():
  """This test is for testing parsing of args and kwargs and `.join()` method"""
  new = Thread(
    target = _dummy_target_raiseToPower,
    args = [4],
    kwargs = { 'power': 2 }
  )
  new.start()
  s = new.join()
  assert s.status == 'Thread terminated'
  assert new.result == 16

def test_threadingThreadParsing():
  """This test is for testing parsing arguments to `threading.Thead`"""
  new = Thread(
    target = _dummy_target_raiseToPower,
    args = [4, 2, 5],
    name = 'testingThread',
    daemon = True
  )
  new.start()
  assert new._thread and new._thread.name == 'testingThread'

def test_suppressAll():
  """This test is for testing that errors are suppressed properly"""
  new = Thread(
    target = _dummy_raiseException,
    args = [ValueError()],
    suppress_errors = True,
    daemon = True
  )
  new.start()
  new.join()
  assert len(new.errors) == 1
  assert isinstance(new.errors[0], ValueError)

def test_ignoreSpecificError():
  """This test is for testing that specific errors are ignored properly"""
  new = Thread(
    target = _dummy_raiseException,
    args = [ValueError()],
    ignore_errors = [ValueError],
  )
  new.start()
  new.join()
  assert len(new.errors) == 0




# >>>>>>>>>> Raising Exceptions <<<<<<<<<< #
def test_raises_notInitializedError():
  """This test should raise ThreadNotInitializedError"""
  new = Thread(
    target = _dummy_target_raiseToPower,
    args = [4, 2]
  )

  with pytest.raises(exceptions.ThreadNotInitializedError):
    new.result

def test_raises_stillRunningError():
  """This test should raise ThreadStillRunningError"""
  new = Thread(
    target = _dummy_target_raiseToPower,
    args = [4, 2, 5]
  )
  new.start()

  with pytest.raises(exceptions.ThreadStillRunningError):
    new.result

def test_raises_ignoreSpecificError():
  """This test is for testing that non-specified errors are not ignored"""
  new = Thread(
    target = _dummy_raiseException,
    args = [FileExistsError()],
    ignore_errors = [ValueError],
    suppress_errors = False
  )
  with pytest.raises(FileExistsError):
    new.start()
    new.join()

def test_raises_HookError():
  """This test should raise """
  new = Thread(
    target = _dummy_target_raiseToPower,
    args = [4, 2]
  )

  def newhook(x: int):
    raise RuntimeError()
  new.add_hook(newhook)

  with pytest.raises(exceptions.HookRuntimeError):
    new.start()
    new.join()