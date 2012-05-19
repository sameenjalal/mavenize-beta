import datetime
from itertools import islice, chain

def get_rating_field(rating):
    """
    Returns the model field that corresponds to an integer rating.
    """
    rating_choices = ['one', 'two', 'three', 'four']
    return rating_choices[rating-1] + '_star'

def decrement_popularities(timestamp, rating):
    """
    Calculates which popularities to decrement based on the timestamp
    of the object being deleted.
    """
    popularity = { 'today': -rating, 'week': -rating, 'month': -rating,
        'alltime': -rating }
    now = datetime.datetime.now()
    if timestamp < now - datetime.timedelta(days=1):
        popularity['today'] = 0
    if timestamp < now - datetime.timedelta(days=7):
        popularity['week'] = 0
    if timestamp < now - datetime.timedelta(days=30):
        popularity['month'] = 0
    return popularity
        

def pop_empty_keys(dictionary):
    """
    Pops the empty keys of a dictiionary.
    """
    for key in dictionary.keys():
        if not dictionary[key] or dictionary[key] == ['']:
            dictionary.pop(key)
    return dictionary

def pair_keys(list_of_dicts, first_key, second_key):
    """
    CURRENTLY UNUSED.
    Pairs a list of dictionaries with two key-value pairs so that the
    value of the first key is now the new key, and the value of the 
    second key is the new value.
    """
    return [{ dictionary[first_key]: dictionary[second_key] } 
        for dictionary in list_of_dicts]

class QuerySetChain(object):
    """
    Chains multiple subquerysets (possibly of different models) and behaves as
    one queryset.  Supports minimal methods needed for use with
    django.core.paginator.
    """

    def __init__(self, *subquerysets):
        self.querysets = subquerysets

    def count(self):
        """
        Performs a .count() for all subquerysets and returns the number of
        records as an integer.
        """
        return sum(qs.count() for qs in self.querysets)

    def _clone(self):
        "Returns a clone of this queryset chain"
        return self.__class__(*self.querysets)

    def _all(self):
        "Iterates records in all subquerysets"
        return chain(*self.querysets)

    def __getitem__(self, ndx):
        """
        Retrieves an item or slice from the chained set of results from all
        subquerysets.
        """
        if type(ndx) is slice:
            return list(islice(self._all(), ndx.start, ndx.stop, ndx.step or 1))
        else:
            return islice(self._all(), ndx, ndx+1).next()
