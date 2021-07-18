import { Component } from '@angular/core'
import { AuthService } from '@/auth/services/auth.service'
import { UserAuth } from '@/auth/models/userAuth'
import { AuthResult } from '@/auth/models'


@Component( {
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: [ './login.component.scss' ]
} )
export class LoginComponent
{
    userAuth: UserAuth
    authResult: AuthResult | null

    constructor( private service: AuthService )
    {
        this.userAuth = {
            email: '',
            password: ''
        }
        this.authResult = null
    }

    auth(): void
    {
        this.authResult = this.service.auth( this.userAuth )
    }

    isValid(): boolean
    {
        // TODO enforce email regex check
        return !!( this.userAuth.password && this.userAuth.email )
    }
}
