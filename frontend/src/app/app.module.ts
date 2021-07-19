import { NgModule } from '@angular/core'
import { StoreModule } from '@ngrx/store'
import { EffectsModule } from '@ngrx/effects'
import { StoreDevtoolsModule } from '@ngrx/store-devtools'
import { SharedModule } from '@/shared/shared.module'
import { LayoutModule } from '@/layout/layout.module'
import { AuthModule } from '@/auth/auth.module'
import { OlympiadsModule } from '@/olympiads/olympiads.module'
import { AppRoutingModule } from '@/app-routing.module'
import { reducers } from '@/reducers'
import { AppEffects } from '@/reducers/app.effects'
import { environment } from '@environments/environment'
import { AppComponent } from '@/app.component'


@NgModule( {
    declarations: [
        AppComponent
    ],
    imports: [
        SharedModule,
        LayoutModule,
        AuthModule,
        OlympiadsModule,
        AppRoutingModule,
        StoreModule.forRoot( reducers ),
        EffectsModule.forRoot( [ AppEffects ] ),
        environment.production ? [] : StoreDevtoolsModule.instrument()
    ],
    providers: [],
    bootstrap: [ AppComponent ]
} )
export class AppModule {}