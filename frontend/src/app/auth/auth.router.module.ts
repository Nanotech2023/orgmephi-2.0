import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { LoginComponent } from '@/auth/components/login/login.component'
import { RegisterComponent } from '@/auth/components/register/register.component'
import { ResetPasswordComponent } from '@/auth/components/reset-password/reset-password.component'
import {
    ResetPasswordConfirmComponent
} from '@/auth/components/reset-password-confirm/reset-password-confirm.component'
import { ResetPasswordTokenComponent } from '@/auth/components/reset-password-token/reset-password-token.component'
import { ConfirmAccountTokenComponent } from '@/auth/components/confirm-account-token/confirm-account-token.component'


const routes: Routes =
    [
        {
            path: 'login',
            component: LoginComponent
        },
        {
            path: 'register',
            component: RegisterComponent
        },
        {
            path: 'reset-password',
            component: ResetPasswordComponent
        },
        {
            path: 'reset-password/confirm',
            component: ResetPasswordConfirmComponent
        },
        {
            path: 'reset-password/token',
            component: ResetPasswordTokenComponent
        },
        {
            path: 'confirm-account',
            component: ConfirmAccountTokenComponent
        }
    ]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ]
} )
export class AuthRouterModule {}
