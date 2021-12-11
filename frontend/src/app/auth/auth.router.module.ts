import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { LoginComponent } from '@/auth/components/login/login.component'
import { RegisterComponent } from '@/auth/components/register/register.component'
import { ResetPasswordComponent } from '@/auth/components/reset-password/reset-password.component'
import {
    ResetPasswordConfirmComponent
} from '@/auth/components/reset-password-confirm/reset-password-confirm.component'


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
            path: 'reset-password-confirm',
            component: ResetPasswordConfirmComponent
        }
    ]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ]
} )
export class AuthRouterModule {}
