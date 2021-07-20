import { Component, OnInit } from '@angular/core'
import { AuthService } from '@/auth/services/auth.service'
import { UserAuth } from '@/auth/models/userAuth'
import { AuthResult } from '@/auth/models'
import { Store } from '@ngrx/store'
import { AuthActions, AuthSelectors, AuthState } from '@/auth/store'
import { Observable } from 'rxjs'
import { selectAuthResult } from '@/auth/store/auth.selectors'


@Component( {
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: [ './login.component.scss' ]
} )
export class LoginComponent implements OnInit
{
    loginAttemptUser: UserAuth
    authResult$!: Observable<AuthResult>

    constructor( private readonly store: Store<AuthState.State> )
    {
        this.loginAttemptUser = {
            email: '',
            password: ''
        }
    }

    ngOnInit(): void
    {
        this.authResult$ = this.store.select( AuthSelectors.selectAuthResult )
    }

    login( loginAttemptUser: UserAuth ): void
    {
        this.store.dispatch( AuthActions.loginAttempt( { user: loginAttemptUser } ) )
    }

    isValid( loginAttemptUser: UserAuth ): boolean
    {
        // TODO enforce email regex check
        return !!( loginAttemptUser.password && loginAttemptUser.email )
    }
}
