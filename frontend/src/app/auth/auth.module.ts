import { NgModule } from '@angular/core'
import { SharedModule } from '@/shared/shared.module'
import { EffectsModule } from '@ngrx/effects'
import { StoreModule } from '@ngrx/store'
import { AuthEffects, AuthState } from '@/auth/store'
import { LoginComponent } from '@/auth/components/login/login.component'
import { RegisterComponent } from '@/auth/components/register/register.component'
import { AuthRouterModule } from '@/auth/auth.router.module'
import { RegisterSchoolComponent } from '@/auth/components/register-school/register-school.component'
import { ResetPasswordComponent } from '@/auth/components/reset-password/reset-password.component'
import {
    ResetPasswordConfirmComponent
} from '@/auth/components/reset-password-confirm/reset-password-confirm.component'


const COMPONENTS = [
    RegisterComponent,
    LoginComponent,
    RegisterSchoolComponent,
    ResetPasswordComponent,
    ResetPasswordConfirmComponent
]


@NgModule( {
    declarations: COMPONENTS,
    imports: [
        SharedModule,
        StoreModule.forFeature( AuthState.featureKey, AuthState.reducer ),
        EffectsModule.forFeature( [ AuthEffects ] ),
        AuthRouterModule
    ]
} )
export class AuthModule {}
