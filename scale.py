import numpy as np
from numpy import ma
import matplotlib as mpl
from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms
from matplotlib.ticker import FixedLocator, ScalarFormatter, NullFormatter


class PiecewiseScale(mscale.ScaleBase):
    name = 'piecewise-linear'

    def __init__(self, axis, fractions, values):
        super().__init__(axis)
        self.fractions = fractions
        self.values = values

    def get_transform(self):
        return PiecewiseScale.PiecewiseLinearTransform(self.values, self.fractions)

    def set_default_locators_and_formatters(self, axis):
        axis.set(major_locator=FixedLocator(np.array(self.values)),)  # TODO
        axis.set_major_formatter(ScalarFormatter())
        axis.set_minor_formatter(NullFormatter())

    def limit_range_for_scale(self, vmin, vmax, minpos):
        return self.values[0], self.values[-1]

    class PiecewiseLinearTransform(mtransforms.Transform):
        input_dims = output_dims = 1

        def __init__(self, xs, ys):
            mtransforms.Transform.__init__(self)
            self.xs = np.array(xs)
            self.ys = np.array(ys)
            assert len(self.xs.shape) == 1
            assert len(self.ys.shape) == 1

        def transform_non_affine(self, x):
            # some checks
            if len(x) == 0:
                return x
            invalid = (x < self.xs[0]) | (x > self.xs[-1])
            x = ma.masked_where(invalid, x)
            x = x.filled(self.xs[0])

            assert all(x >= self.xs[0])
            lower_ind = sum((x > boundary).astype(int) for boundary in self.xs[1:])
            lower_x = self.xs[lower_ind]
            upper_x = self.xs[lower_ind+1]
            lower_y = self.ys[lower_ind]
            upper_y = self.ys[lower_ind+1]
            frac = (x - lower_x) / (upper_x - lower_x)
            result = upper_y * frac + lower_y * (1-frac)
            return ma.masked_where(invalid, result)

        def inverted(self):
            return PiecewiseScale.PiecewiseLinearTransform(self.ys, self.xs)

mscale.register_scale(PiecewiseScale)
