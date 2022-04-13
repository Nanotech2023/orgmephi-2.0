import { NgModule } from '@angular/core'
import { SharedModule } from '@/shared/shared.module'
import { EffectsModule } from '@ngrx/effects'
import { StoreModule } from '@ngrx/store'
import { AuthEffects, AuthState } from '@/auth/store'
import { RouterModule } from '@angular/router'
import { AUTH_COMPONENTS, AUTH_ROUTES } from '@/auth/auth.module.components'


@NgModule( {
    declarations: AUTH_COMPONENTS,
    imports: [
        SharedModule,
        StoreModule.forFeature( AuthState.featureKey, AuthState.reducer ),
        EffectsModule.forFeature( [ AuthEffects ] ),
        RouterModule.forChild( AUTH_ROUTES )
    ]
} )
export class AuthModule {}
