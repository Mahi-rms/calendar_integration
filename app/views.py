from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from calendar_integration import settings
import google_auth_oauthlib.flow
import google.oauth2.credentials
import googleapiclient.discovery
from helpers.views_helper import generate_response
from helpers.enum_helper import Messages
# Create your views here.
api_constants=settings.APIConstants()

@api_view(['GET'])
def GoogleCalendarInitView(request):
    try:
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file=api_constants.CLIENT_SECRETS_FILE,
        scopes=api_constants.SCOPES)

        flow.redirect_uri = api_constants.REDIRECT_URI
        auth_uri, state = flow.authorization_url()
        request.session['state'] = state

        return Response(generate_response(message=Messages.INITIATION_SUCCESSFUL,auth_uri=auth_uri))
    except Exception as exp:
        return Response(generate_response(message=Messages.SOME_ERROR_OCCURRED, error=exp))


@api_view(['GET'])
def GoogleCalendarRedirectView(request):
    try:
        state = request.session['state']
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            client_secrets_file=api_constants.CLIENT_SECRETS_FILE, 
            scopes=api_constants.SCOPES, 
            state=state)
        flow.redirect_uri = api_constants.REDIRECT_URI

        authorization_response = request.get_full_path()
        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials
        credentials = google.oauth2.credentials.Credentials(
            client_id= credentials.client_id,
            client_secret=credentials.client_secret,
            token=credentials.token,
            refresh_token=credentials.refresh_token,
            token_uri=credentials.token_uri,
            scopes=credentials.scopes)

        client = googleapiclient.discovery.build(
            api_constants.API_SERVICE_NAME, api_constants.API_VERSION, credentials=credentials)

        calendar_list = client.calendarList().list().execute()
        calendar_id = calendar_list['items'][0]['id']
        events  = client.events().list(calendarId=calendar_id).execute()
        events_record= []
        if events['items']:
            for record in events['items']:
                events_record.append(record)
            return Response(generate_response(message=Messages.EVENTS_LIST,events=events_record))
        else:
            return Response(generate_response(message=Messages.DATA_NOT_FOUND))
    except Exception as exp:
        return Response(generate_response(message=Messages.SOME_ERROR_OCCURRED, error=exp))

