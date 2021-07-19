import { NgModule } from '@angular/core'
import { RegisterComponent } from './components/register/register.component'
import { LoginComponent } from './components/login/login.component'
import { SharedModule } from '@/shared/shared.module'


const COMPONENTS = [
    RegisterComponent,
    LoginComponent
]


@NgModule( {
    declarations: COMPONENTS,
    imports: [
        SharedModule
    ]
} )
export class AuthModule {}
