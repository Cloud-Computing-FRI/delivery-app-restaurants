{{/*
Template helpers for the restaurants chart.

By default the Service name is the bare chart name ("restaurants"), NOT a
release-prefixed name, so sibling services (and the UI) can address it at a
stable DNS name. Set fullnameOverride to change it.
*/}}

{{- define "restaurants.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "restaurants.fullname" -}}
{{- default (include "restaurants.name" .) .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "restaurants.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/* Common labels. Call with the root context ($). */}}
{{- define "restaurants.labels" -}}
helm.sh/chart: {{ include "restaurants.chart" . }}
app.kubernetes.io/part-of: delivery-app
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/* Selector labels. Call with the root context ($). */}}
{{- define "restaurants.selectorLabels" -}}
app.kubernetes.io/name: {{ include "restaurants.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: restaurants
{{- end -}}

{{/* Host of the database: the in-cluster service unless database.host overrides it. */}}
{{- define "restaurants.dbHost" -}}
{{- if .Values.database.host -}}
{{- .Values.database.host -}}
{{- else -}}
{{- printf "%s-db" (include "restaurants.fullname" .) -}}
{{- end -}}
{{- end -}}

{{/* Name of the Secret holding DATABASE_URL (pre-created one in prod). */}}
{{- define "restaurants.dbSecret" -}}
{{- default (printf "%s-db" (include "restaurants.fullname" .)) .Values.database.existingSecret -}}
{{- end -}}
