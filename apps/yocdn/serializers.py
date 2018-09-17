# -*- coding: utf-8 -*-
from yocdn import models
from yocdn.tasks import refresh_cdn
from django.conf import settings
from rest_framework import serializers

__all__ = [

]


class YoCDNSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CDN
        fields = (
            'id', 'uuid', 'url', 'type', 'create_time', 'status', 'process'
        )
        read_only_fields = (
            'id', 'uuid', 'create_time', 'status'
        )

    def create(self, validated_data):
        obj = super(YoCDNSerializer, self).create(validated_data)
        refresh_cdn.delay(obj)
        return obj


class YoCDNListSerializer(serializers.Serializer):
    cdns = serializers.ListSerializer(child=YoCDNSerializer())
    class Meta:
        fields = (
            'cdns'
        )
    def create(self, validated_data):
        user = self.context['request'].user
        for obj in validated_data['cdns']:
            obj.user = user
            ser = YoCDNSerializer(data=obj)
            if ser.is_valid():
                print(ser.save())
        return {'cdns':{}}


'''
{
    "cdns": [
        {"url":"https://www.baidu.com", "type":3},
        {"url":"https://www.baidu.com", "type":3},
        {"url":"https://www.baidu.com", "type":3}
    ]
}
'''