import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { LoginComponent } from '@/auth/components/login/login.component'
import { RegisterComponent } from '@/auth/components/register/register.component'
import { NoAuthGuardService } from '@/shared/noauth.guard.service'


const routes: Routes =
    [
        {
            path: 'login',
            component: LoginComponent,
            // canActivate: [ NoAuthGuardService ]
        },
        {
            path: 'register',
            component: RegisterComponent,
            // canActivate: [ NoAuthGuardService ]
        }
    ]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ]
} )
export class AuthRouterModule {}
