
.. image:: logo.png


Python Project *GeolocationUpdate*
-----------------------------------------------------------------------


Introduction
------------

To import the project simply type

.. code-block:: python

    >>> import GeolocationUpdate

after installation.


Install
-------

The latest stable version can always be installed or updated via pip:

.. code-block:: bash

    $ pip install GeolocationUpdate



Theory
------
With this project, we want to be able to find the speed limit and a tuple of matching way objects of a users location. The input information we can use are: The current langitude, longitude, direction and speed of the user.
There are a few steps, on how we find the possible solution. Afterwards, we want to discuss on how accurate this solution is.

1) First of all, we create a location object $pointSelf$ out of the information about the users current location. This object contains the information about the users latitude, longitude, speed and direction.
2) Then, we create a few more location objects: Three location objects $pSelfF, pSelfPP, pSelfPPP$ in front of the user and three location objects $pSelfP, pSelfPP, pSelfPPP$ right behind the user. Every points distance to their direct neighbours counts five meters.
3) Now, we want to get a list of ways $allWays$ to compare our Locations with and find the possible way that the user is on. Because we do not want too much traffic on the server, we start with a relativily small radius and expand the radius (in meters) for the request only if needed. After calling the function $get\_ways$, we receive a list of suitable ways $allWays$.
4) For every Location we created in step 1) and 2), we calculate a quality Level for every way in $allWays$. This quality Level depends on the shortest distance of the location to the way and the degree difference from direction to the location to the direction of the way.
5) Afterwards, we compute the qualityLevel $qL$ of every users location $pointSelf$ from step 1). To get that qualityLevel $qL$, we process each location object from step 1) and 2) into one qualityLevel.
6) Also, if the way was the pick we made during the last request, we set $qL := qL * 0.5$.
7) At last, we sort the ways depending on ascending qualityLevels. From that, we get our return value: The limit of the first way in that list and also the tuple that contains every way.


Accuracy
--------

1) Straight Street

.. image:: statics/traubenwegGerade.png
  :width: 400
  :alt: Straight Way

2) Street with corners

.. image:: statics/imFiedlersee.png
  :width: 400
  :alt: Street with corners

License
-------

Code and documentation are available according to the license
(see LICENSE file in repository).
