from fastapi import HTTPException, status, Request
from .mail_communicator import MailCommunicator
from typing import List
from py2neo_schemas.nodes import User
from app.globals import APP_NAME


    
class AccountActivationHandler:
    
    @classmethod
    def send_activation_mail(self, user: User, activation_code : str, request : Request) -> bool:
        
        activation_link = request.url.scheme + "://" + request.url.netloc + "/activate/" + activation_code
        templates = self.generate_activation_mail(user, activation_link)
        subject=f"[{APP_NAME}] Account activation"
        recipient=user.email
        try:
            MailCommunicator.send_mail(recipient, subject, templates)
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong while sending the mail"
            )

    @classmethod
    def send_update_address_mail(self, user: User, activation_code : str, recipient_address: str, request : Request) -> bool:
        
        activation_link = request.url.scheme + "://" + request.url.netloc + "/dashboard/profile/email/confirm/" + activation_code
        templates = self.generate_update_address_mail(user, activation_link)
        subject=f"[{APP_NAME}] Account email address update"
        recipient=recipient_address
        try:
            MailCommunicator.send_mail(recipient, subject, templates)
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong while sending the mail"
            )

    @classmethod
    def generate_activation_mail(self, user:User, activation_link : str) -> dict:
        # return the mail created
        
        html_template = f"""
        <div class="container" style="text-align: center;">
            <p style="font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; text-align: center; font-size: 1.5rem;">Hello <span style="font-weight: bold; text-transform: capitalize;">{user.login}</span></p>
            <p style="font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; text-align: center; font-size: 1.5rem;">There is one last step to get your account on {APP_NAME}. Just click on this activation button</p>

            <a href="{activation_link}"><button style="font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; font-size: 1.5rem; background-color: rgb(0, 195, 255); padding: 0.7rem 1rem; color: white; border: 0; border-radius: 4px; box-shadow: 0 0 4px #ccc;">Activate account</button></a>
        </div>
		"""
        text_template = f"""
            Hello {user.login}
            There is one last step to get your account on {APP_NAME}. Just click on this activation link
            You can also copy it and paste it in your navigator's address bar
            
            {activation_link}
		"""
        return {
            "html_template" : html_template,
            "text_template" : text_template
        }
        
    @classmethod
    def generate_update_address_mail(self, user:User, update_address_link : str) -> dict:
        
        html_template = f"""
            <div class="container" style="text-align: center;">
                <p style="font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; text-align: center; font-size: 1.5rem;">Hello <span style="font-weight: bold; text-transform: capitalize;">{user.login}</span></p>
                <p style="font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; text-align: center; font-size: 1.5rem;">You've attempted to replace your {APP_NAME} account email address by this one. Click on the link bellow to validate it, of just ignore it if you are not {user.login}</p>

                <a href="{update_address_link}"><button style="font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; font-size: 1.5rem; background-color: rgb(0, 195, 255); padding: 0.7rem 1rem; color: white; border: 0; border-radius: 4px; box-shadow: 0 0 4px #ccc;">Update Address</button></a>
            </div>
		"""
        text_template = f"""
            Hello {user.login}
            You've attempted to replace your {APP_NAME} account email address by this one. Click on the link bellow to validate it, of just ignore it if you are not {user.login}
            
            {update_address_link}
		"""
        return {
            "html_template" : html_template,
            "text_template" : text_template
        }
    
    