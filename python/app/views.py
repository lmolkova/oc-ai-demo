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

service_name = os.getenv('SERVICE_NAME', 'python-service')
config_integration.trace_integrations(INTEGRATIONS, tracer=tracer_module.Tracer(
    exporter=trace_exporter.TraceExporter(
        service_name=service_name,
        endpoint=os.getenv('OCAGENT_TRACE_EXPORTER_ENDPOINT'),
        transport=BackgroundThreadTransport),
    propagator=TraceContextPropagator()))


def call_go_app(request):
    requests.get("http://go-app:50030/call_aspnetcore_app")

    return HttpResponse("hello world from " + service_name)
