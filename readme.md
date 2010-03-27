Ramblings to be organized later..

99% of this will never happen, this is just my project init tool, in short.

## Notes

* Gig should automatically check for a .gig file in current or all parent directories to find the root of the project
* Said .gig file can contain basic settings for the project, eg, apps to be installed.
* Format is .. ini?

    [apps]
    http://bitbucket.org/jdriscoll/django-imagekit/
    MySQLdb


## Usage Ideas

Start a basic django project

    $ gig init project

Install some stuff into it

    $ gig add django

where does that come from? What if I want trunk?

    $ gig add --trunk django

Install imagekit from Mercurial

    $ gig add http://bitbucket.org/jdriscoll/django-imagekit/

understands bitbucket and github URLs, otherwise:

    $ gig add --hg http://bitbucket.org/jdriscoll/django-imagekit

or maybe

    $ gig add hg+http://bitbucket.org/jdriscoll/django-imagekit

Start a project based on "imagekit" project template?

    $ gig init -t imagekit project
