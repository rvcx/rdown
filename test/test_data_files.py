import rdown
import glob
import os.path

def pytest_generate_tests(metafunc):
  mfns = glob.glob('test/data/*.mdown')
  data = []
  for mfn in mfns:
    fn, _ = os.path.splitext(mfn)
    rfn = fn + '.rline'
    if os.path.isfile(rfn):
      with open(mfn) as mf, open(rfn) as rf:
        m, r = mf.read(), rf.read()
        data.append((m, r))
  metafunc.parametrize(['mdown', 'rline'], data )

def test_knownoutput(mdown, rline):
  assert rdown.markdown(mdown).strip() == rline.strip()