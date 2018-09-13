# Copyright 2017, OpenCensus Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.http import HttpResponse
from django.shortcuts import render

from .forms import HelloForm

from opencensus.trace import config_integration
from opencensus.trace.exporters.ocagent import trace_exporter
from opencensus.trace import tracer as tracer_module
from opencensus.trace.propagation.trace_context_http_header_format import TraceContextPropagator
from opencensus.trace.exporters.transports.background_thread \
    import BackgroundThreadTransport

import time
import os
import requests


INTEGRATIONS = ['httplib']

config_integration.trace_integrations(INTEGRATIONS, tracer=tracer_module.Tracer(
    exporter=trace_exporter.TraceExporter(
        service_name=os.getenv('SERVICE_NAME', 'python-service'),
        endpoint=os.getenv('OCAGENT_TRACE_EXPORTER_ENDPOINT'),
        transport=BackgroundThreadTransport),
    propagator=TraceContextPropagator()))


def home(request):
    return render(request, 'home.html')


def call_dotnet_app(request):
    data = [{"url": "http://blank.org", "arguments": []}]
    response = requests.post(
        "http://aspnetcore-app/api/forward", json=data)

    return HttpResponse(str(response.status_code))


def call_go_app(request):
    response = requests.get("http://go-app/")

    return HttpResponse(str(response.status_code))


def call_blank(request):
    response = requests.get("http://blank.org/")

    return HttpResponse(str(response.status_code))


def buy(request):
    response = requests.get(
        "https://acmefrontend.azurewebsites.net/api/buywidget")

    return HttpResponse(str(response.status_code))


def health_check(request):
    return HttpResponse("ok", status=200)
