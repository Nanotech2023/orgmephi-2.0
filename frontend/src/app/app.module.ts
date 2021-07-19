import { NgModule } from '@angular/core'
import { AppRoutingModule } from '@/app-routing.module'
import { AppComponent } from '@/app.component'
import { LayoutModule } from '@/layout/layout.module'
import { OlympiadsModule } from '@/olympiads/olympiads.module'
import { SharedModule } from '@/shared/shared.module'
import { AuthModule } from '@/auth/auth.module'
import { UsersModule } from '@/users/users.module'


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
        AppRoutingModule
    ],
    providers: [],
    bootstrap: [ AppComponent ]
} )
export class AppModule
{
}