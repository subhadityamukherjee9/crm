from haystack import indexes
from .models import Contacts, Tags, CompanyAssociation, Company, Institute, InsttitueAssociation
from haystack.management.commands import update_index
update_index.Command().handle()

class ContactsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    location = indexes.CharField(model_attr='location')
    title = indexes.CharField(model_attr='title')
    tags = indexes.CharField()
    company = indexes.CharField()
    institute = indexes.CharField()

    def prepare_tags(self, Contacts):
        return [auth.tag_name for auth in Contacts.tags.all()]

    def prepare_company(self, Contacts):
        return [auth.company.company_name for auth in Contacts.company.all()]

    def prepare_institute(self, Contacts):
        return [auth.institute.institute_name for auth in Contacts.institute.all()]

    def get_model(self):
        return Contacts

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
