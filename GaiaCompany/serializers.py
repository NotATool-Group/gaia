from rest_framework.serializers import ModelSerializer

from GaiaCompany.models import Company


class CompanySerializer(ModelSerializer):

    def __init__(self, *args, include_dataset=False, **kwargs):
        """
        Custom constructor to dynamically add the dataset field to the serializer if required.

        The dataset field is not included by default, because it can be very large and it is not always needed.
        If the dataset field is required, it can be included by passing the include_dataset=True parameter during the
        serializer initialization.

        @param include_dataset: whether to include the dataset field in the serializer
        """
        super().__init__(*args, **kwargs)
        if not include_dataset:
            self.fields.pop("dataset", None)

    class Meta:
        model = Company
        fields = ("id", "name", "dataset", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
