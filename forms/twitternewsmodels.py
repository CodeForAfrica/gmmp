from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelutils import *

class TwitterJournalist(models.Model):
    # Journalists / Reporters
    sex = models.PositiveIntegerField(choices=GENDER, verbose_name=_('Journalist''s Sex'))
    tbl = dict(GENDER)
    twitter_sheet = models.OneToOneField('TwitterSheet')

    def __unicode__(self):
        return u"%s" % (self.tbl[self.sex])

class TwitterPerson(models.Model):
    # Setting the unicode to blank in the admin
    sex = models.PositiveIntegerField(choices=GENDER, verbose_name=_('Sex'))
    is_photograph = models.PositiveIntegerField(choices=IS_PHOTOGRAPH, verbose_name=_('Photo/Video of person attached'))
    twitter_sheet = models.ForeignKey('TwitterSheet')

class TwitterSheet(SheetModel):
    class Meta:
        verbose_name = _('Twitter Submission')

    media_name = models.CharField(max_length=255, verbose_name=_('Media Name'), help_text=_('''For example. 'CNN Breaking News' '''))
    twitter_handle = models.CharField(max_length=255, verbose_name=_('Twitter Handle'), help_text=_('e.g. https://twitter.com/cnnbrk'))

    # Story
    retweet = models.PositiveIntegerField(choices=RETWEET, 
        verbose_name=_('Tweet or Retweet'),
        help_text=_('Only retweets from the same media house can be coded. Do not code retweets from other news providers')
    )
    topic = models.PositiveIntegerField(choices=TOPICS, help_text=_('''Within each broad category, we include a code for 'other stories'. Please use these codes only as a last resort.'''), verbose_name=_('Topic'))
    comments = models.TextField(verbose_name=_('Describe any photographs, images, other multimedia components included in the tweet and the conclusions you draw from them.'), blank=True)
    url_and_multimedia = models.TextField(verbose_name=_('Copy and paste the URL of the story. Describe any photographs, images, other multimedia features included in the story. Note down the conclusions you draw from the images, audio and video..'), blank=True)

    # Analysis
    about_women = models.CharField(max_length=1, choices=YESNO, verbose_name=_('Is the story about a particular woman or group of women?'))
    stereotypes = models.PositiveIntegerField(choices=AGREE_DISAGREE, verbose_name=_('This story clearly challenges gender stereotypes'))
    further_analysis = models.CharField(max_length=1, choices=YESNO, verbose_name=_('Does this tweet warrant further analysis?'), help_text=_('<br><br>A tweet warrants further analysis if it clearly perpetuates or clearly challenges gender stereotypes, if it presents the story being tweeted in a sensationalist, gender-biased manner, etc . Consult the guide for further explanation<br>If you select Yes, you will need to send a print-out of the tweet and screen grab of the page to your national/regional coordinator.'))

