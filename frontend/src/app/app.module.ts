import { NgModule } from '@angular/core'
import { StoreModule } from '@ngrx/store'
import { EffectsModule } from '@ngrx/effects'
import { StoreDevtoolsModule } from '@ngrx/store-devtools'
import { SharedModule } from '@/shared/shared.module'
import { LayoutModule } from '@/layout/layout.module'
import { AuthModule } from '@/auth/auth.module'
import { OlympiadsModule } from '@/olympiads/olympiads.module'
import { AppRoutingModule } from '@/app-routing.module'
import { environment } from '@environments/environment'
import { AppComponent } from '@/app.component'
import { UsersModule } from '@/users/users.module'
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'
import { AuthService } from '@/auth/api/auth.service'
import { ManageOlympiadsModule } from '@/manage-olympiads/manage-olympiads.module'
import { ManageUsersModule } from '@/manage-users/manage-users.module'
import { OlympiadsServiceMock } from '@/manage-olympiads/api/olympiads.service.mock'
import { OlympiadsService } from '@/manage-olympiads/api/olympiads.service'


@NgModule( {
    declarations: [
        AppComponent
    ],
    imports: [
        SharedModule,
        LayoutModule,
        AuthModule,
        OlympiadsModule,
        UsersModule,
        ManageUsersModule,
        ManageOlympiadsModule,
        AppRoutingModule,
        StoreModule.forRoot( {} ),
        EffectsModule.forRoot( [] ),
        environment.production ? [] : StoreDevtoolsModule.instrument(),
        BrowserAnimationsModule
    ],
    providers: [
        { provide: AuthService },
        { provide: OlympiadsService, useClass: OlympiadsServiceMock }
    ],
    bootstrap: [ AppComponent ]
} )
export class AppModule {}