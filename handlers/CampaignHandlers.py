from models.CampaignModel import Campaign
from handlers.BaseHandlers import BaseHandler

from libs.SecurityDecorators import *


class CampaignIndexHandler(BaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        campaigns = Campaign.all()
        self.render('campaign/index.html', campaigns=campaigns)