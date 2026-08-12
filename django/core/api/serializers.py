#   ./django/core/api/serializers.py


from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    # Um serializer base que fornece validação e serialização padrão.

    def validate(self, attrs):
        # Valida os atributos do serializer.
        return super().validate(attrs)


class MessageSerializer(serializers.Serializer):
    # Um serializer para mensagens de resposta.

    message = serializers.CharField()


class SuccessSerializer(serializers.Serializer):
    # Um serializer para mensagens de sucesso.

    success = serializers.BooleanField(
        default=True,
    )
