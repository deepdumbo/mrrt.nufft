from __future__ import division, print_function, absolute_import

import numpy as np
from numpy.testing import (run_module_suite, assert_raises, assert_)

from pyir.nufft.nufft import NufftKernel

kernel_types = ['kb:beatty', 'kb:minmax', 'minmax:kb', 'linear', 'diric']


def test_kernel(show_figure=False):

    # can call with mixtures of integer, list or array input types
    d2 = NufftKernel('kb:beatty', Kd=[32, 32], Jd=[4, 4], Nd=[24, 16])
    d3 = NufftKernel('kb:minmax', Kd=[32, 32], Jd=4, Nd=np.asarray([24, 16]))
    d4 = NufftKernel('minmax:kb',
                     Kd=[32, 32], Jd=4, Nd=[24, 16], Nmid=[12, 8])
    d1 = NufftKernel('linear', ndim=2, Jd=4)
    d5 = NufftKernel('diric', ndim=1, Kd=32, Jd=32, Nd=16)

    # invalid kernel raises ValueError
    assert_raises(ValueError, NufftKernel, 'foo', ndim=2, Jd=4)

    if show_figure:
        axes = d2.plot()
        d3.plot(axes)
        d4.plot(axes)
        d1.plot(axes)
        d5.plot()


def test_kernel_range(show_figure=False):
    Jd = np.asarray([3, 4])
    kernel_types = ['kb:beatty', ]
    for ktype in kernel_types:
        kernel = NufftKernel(ktype,
                             ndim=2,
                             Nd=[64, 64],
                             Jd=Jd,
                             Kd=[128, 128],
                             Nmid=[32, 32])

        for d in range(kernel.ndim):
            # non-zero within extent of J
            x = np.linspace(-Jd[d]/2+.001, Jd[d]/2-.001, 100)
            assert_(np.all(kernel.kernel[d](x) > 0))

            # 0 outside range of J
            assert_(kernel.kernel[d](np.asarray([Jd[d]/2, ]))[0] == 0)
            assert_(kernel.kernel[d](np.asarray([-Jd[d]/2, ]))[0] == 0)


if __name__ == '__main__':
    run_module_suite()
