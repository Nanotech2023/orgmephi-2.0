import { NgModule } from '@angular/core'
import { SharedModule } from '@/shared/shared.module'
import { EffectsModule } from '@ngrx/effects'
import { StoreModule } from '@ngrx/store'
import { AuthState, AuthEffects } from '@/auth/store'
import { LoginComponent } from '@/auth/components/login/login.component'
import { RegisterComponent } from '@/auth/components/register/register.component'
import { AuthService } from '@/auth/api/auth.service'
import { AuthServiceMock } from '@/auth/api/auth.service.mock'


const COMPONENTS = [
    RegisterComponent,
    LoginComponent
]


@NgModule( {
    declarations: COMPONENTS,
    imports: [
        SharedModule,
        StoreModule.forFeature( AuthState.featureKey, AuthState.reducer ),
        EffectsModule.forFeature( [ AuthEffects ] )
    ],
    providers: [
        { provide: AuthService, useClass: AuthServiceMock }
    ]
} )
export class AuthModule {}
