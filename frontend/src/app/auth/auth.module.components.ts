import { Routes } from '@angular/router'
import { LoginComponent } from '@/auth/components/login/login.component'
import { RegisterComponent } from '@/auth/components/register/register.component'
import {
    ResetPasswordRequestComponent
} from '@/auth/components/reset-password-request/reset-password-request.component'
import {
    ResetPasswordRequestSendComponent
} from '@/auth/components/reset-password-request-send/reset-password-request-send.component'
import {
    ResetPasswordRequestSuccessComponent
} from '@/auth/components/reset-password-request-success/reset-password-request-success.component'
import {
    ConfirmAccountRequestSuccessComponent
} from '@/auth/components/confirm-account-request-success/confirm-account-request-success.component'
import { ProfileEditComponent } from '@/profile/containers/profile-edit/profile-edit.component'
import { RegisterSchoolComponent } from '@/auth/components/register-school/register-school.component'
import { AuthLayoutComponent } from '@/auth/components/auth-layout/auth-layout.component'
import {
    ConfirmAccountRequestComponent
} from '@/auth/components/confirm-account-request/confirm-account-request.component'
import {
    ConfirmAccountRequestSendComponent
} from '@/auth/components/confirm-account-request-send/confirm-account-request-send.component'
import { AuthLayoutLinksComponent } from '@/auth/components/auth-layout-links/auth-layout-links.component'


export const AUTH_COMPONENTS = [
    AuthLayoutComponent,
    AuthLayoutLinksComponent,
    LoginComponent,
    RegisterComponent,
    RegisterSchoolComponent,
    ResetPasswordRequestComponent,
    ResetPasswordRequestSendComponent,
    ResetPasswordRequestSuccessComponent,
    ConfirmAccountRequestComponent,
    ConfirmAccountRequestSendComponent,
    ConfirmAccountRequestSuccessComponent
]

export const AUTH_ROUTES: Routes =
    [
        {
            path: 'auth', component: AuthLayoutComponent,
            children: [
                {
                    path: '', pathMatch: 'full', redirectTo: 'login'
                },
                {
                    path: 'login',
                    component: LoginComponent
                },
                {
                    path: 'register',
                    component: RegisterComponent
                },
                {
                    path: 'reset-password/request',
                    component: ResetPasswordRequestComponent
                },
                {
                    path: 'reset-password/request-send',
                    component: ResetPasswordRequestSendComponent
                },
                {
                    path: 'reset-password/success',
                    component: ResetPasswordRequestSuccessComponent
                },
                {
                    path: 'confirm-account/request',
                    component: ConfirmAccountRequestComponent
                },
                {
                    path: 'confirm-account/request-send',
                    component: ConfirmAccountRequestSendComponent
                },
                {
                    path: 'confirm-account/success',
                    component: ConfirmAccountRequestSuccessComponent
                }
            ]
        }
    ]