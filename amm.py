class AMM:
    def __init__(self, amount_x, amount_y, m=None):
        self._x = amount_x  # amount of x
        self._y = amount_y  # amount of y
        if m is None:
            self._m = amount_x + amount_y  # money supply
        else:
            self._m = m
        self.k = self._x * self._y  # constant
        self.providers = dict()

    def add_liquidity(self, x, y, provider):
        self.providers[provider] = self.providers.get(provider, {'x': 0, 'y': 0})
        self.providers[provider]['x'] += x
        self.providers[provider]['y'] += y
        self._x += x
        self._y += y
        self.k = self._x * self._y

    def take_liquidity(self, x, y, provider):
        self.providers[provider] = self.providers.get(provider, {'x': 0, 'y': 0})
        assert self.providers[provider]['x'] - x >= 0
        assert self.providers[provider]['y'] - y >= 0
        assert self._x - x > 0
        assert self._y - y > 0
        self.providers[provider]['x'] -= x
        self.providers[provider]['y'] -= y
        self._x -= x
        self._y -= y
        self.k = self._x * self._y


    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        assert value > 0
        self._x = value
        self._y = self.k / self._x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        assert value > 0
        self._y = value
        self._x = self.k / self._y

    @property
    def price_x(self):
        return self.y / (self.m / 2)

    @property
    def price_y(self):
        return self.x / (self.m / 2)

    @property
    def m(self):
        return self._m

    @m.setter
    def m(self, value):
        assert value > 0
        self._m = value

    def __iter__(self):
        return (value for value in (self.x, self.y, self.m))

    def __repr__(self):
        return "AMM\nx:\t  {}\ny:\t  {}\nm:\t  {}\nprice_x:  {}\nprice_y:  {}\n\nproviders: {}".format(
            *map(lambda x: round(x, 2), (self.x, self.y, self.m, self.price_x, self.price_y)), self.providers)


class Customer:
    def __init__(self, x_amount=0, y_amount=0, m_amount=0):
        self.x = x_amount
        self.y = y_amount
        self.m = m_amount

    def offer_x(self, amount, pool: AMM):
        assert self.x - amount >= 0
        prev_y = pool.y
        pool.x += amount
        self.y += prev_y - pool.y

    def offer_y(self, amount, pool: AMM):
        assert self.y - amount >= 0
        prev_x = pool.x
        pool.y += amount
        self.x += prev_x - pool.x

    def offer_liquidity_x(self, amount, pool: AMM):
        assert self.x - amount >= 0
        pool.add_liquidity(x=amount, y=0, provider=self.hash)
        self.x -= amount

    def offer_liquidity_y(self, amount, pool: AMM):
        assert self.y - amount >= 0
        pool.add_liquidity(x=0, y=amount, provider=self.hash)
        self.y -= amount

    def take_liquidity_x(self, amount, pool: AMM):
        pool.take_liquidity(x=amount, y=0, provider=self.hash)
        self.x += amount

    def take_liquidity_y(self, amount, pool: AMM):
        pool.take_liquidity(x=0, y=amount, provider=self.hash)
        self.y += amount

    @property
    def hash(self):
        return hex(hash(self))

    def __repr__(self):
        return "Customer {}\nx:\t{}\ny:\t{}\nmoney:  {}".format(self.hash, self.x, self.y, self.m)

