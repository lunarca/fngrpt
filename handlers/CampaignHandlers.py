from models.CampaignModel import Campaign
from handlers.BaseHandlers import BaseHandler

from libs.SecurityDecorators import *
from models import dbsession

from libs.ValidationError import ValidationError


class CampaignIndexHandler(BaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        campaigns = Campaign.all()
        self.render('campaign/index.html', campaigns=campaigns)


class CampaignCreationHandler(BaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        self._render_page()

    @authenticated
    def post(self, *args, **kwargs):
        name = self.get_argument("name", "")
        description = self.get_argument("description", "")
        endpoint = self.get_argument("endpoint", "")

        user = self.get_current_user()

        try:
            campaign = self.create_campaign(name, endpoint, description, user)
            self.redirect("/campaigns/management/%s" % campaign.uuid)
        except ValidationError as error:
            self._render_page(errors=str(error))

    def _render_page(self, errors=None):
        current_user = self.get_current_user()
        self.render('campaign/new.html',
                    errors=errors,
                    current_user=current_user
                    )

    def create_campaign(self, name, endpoint, description, user):
        campaign = Campaign(name=name, endpoint=endpoint, description=description, user=user)
        dbsession.add(campaign)
        dbsession.commit()
        return campaign


class CampaignManagementHandler(BaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        if len(args) and Campaign.by_uuid(args[0]) is not None:
            campaign = Campaign.by_uuid(args[0])
            self.render('campaign/manage.html', campaign=campaign)
        else:
            self.render('errors/404.html')

    @authenticated
    def post(self, *args, **kwargs):


class CampaignDeletionHandler(BaseHandler):

    @authenticated
    def post(self, *args, **kwargs):
