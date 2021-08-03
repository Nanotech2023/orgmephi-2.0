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
import { UsersModule } from '@/users/users.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'
import { AdminModule } from '@/admin/admin.module'


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
        AdminModule,
        AppRoutingModule,
        StoreModule.forRoot( {} ),
        EffectsModule.forRoot( [] ),
        environment.production ? [] : StoreDevtoolsModule.instrument(),
        BrowserAnimationsModule
    ],
    providers: [],
    bootstrap: [ AppComponent ]
} )
export class AppModule {}