Alertmanager Webhook for Webex Teams
====================================

This programm connects Webex Teams as receiver for messages from
Prometheus Alertmanager.


Installation
------------

1. Create a Bot in [Webex Teams](https://developer.webex.com/my-apps/).
2. Grab the generated `access_token` and invite the Bot in a channel.
3. Call the API for the `room_id`

```
curl -s -X GET -H 'Authorization: Bearer XXXXXXXXXXXXX' https://webexapis.com/v1/rooms | jq .
```

4. Create a K8S secret in the `cattle-monitoring-system` namespace
(or another) with the credentials for Webex:

```
kubectl create secret generic mcsps-webex-receiver -n cattle-monitoring-system \
  --from-literal=WEBEX_TOKEN='XXXXXXXX' \
  --from-literal=WEBEX_ROOM='ZZZZZZZZZZZZ'
```

5. Review namespace settings and apply workload and service to K8S

```
kubectl -n demoapp apply -f kubernetes/deployment.yaml
kubectl -n demoapp apply -f kubernetes/service.yaml
kubectl -n demoapp apply -f kubernetes/alertmanagerconfig.yaml
```


Hints
-----

* Webhook url has the form `<service-name>.<namespace>.<cluster-domain>:port`
Can be adapt in the Receiver and the kubernetes/service.yaml if there is
another location.

* Only some basic labels are handled in webex/webex.py. This can be extend
or more minimized.
Webex API supports [text and markdown message format](https://developer.webex.com/docs/api/basics).

* Feature is [on the way](https://github.com/prometheus-operator/prometheus-operator/pull/5305)
in Prometheus Operator/Alertmanager, so this app will go obseleted


Credits
-------

[@aixeshunter](https://github.com/aixeshunter/alertmanager-webhook)

Frank Kloeker <f.kloeker@telekom.de>

Life is for sharing. If you have an issue with the code or want to improve it,
feel free to open an issue or an pull request.
