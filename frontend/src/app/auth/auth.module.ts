import { NgModule } from '@angular/core'
import { RegisterComponent } from './components/register/register.component'
import { LoginComponent } from './components/login/login.component'
import { SharedModule } from '@/shared/shared.module'


@NgModule( {
    declarations: [
        RegisterComponent,
        LoginComponent
    ],
    imports: [
        SharedModule
    ]
} )
export class AuthModule {}
