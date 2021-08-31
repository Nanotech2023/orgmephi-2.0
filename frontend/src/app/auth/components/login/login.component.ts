import { Component, HostListener, OnInit } from '@angular/core'
import { Store } from '@ngrx/store'
import { AuthActions, AuthSelectors, AuthState } from '@/auth/store'
import { Observable } from 'rxjs'
import { ErrorValue, LoginRequestUser } from '@/auth/api/models'
import { fixedHeight } from '@/shared/consts'


@Component( {
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: [ './login.component.scss' ]
} )
export class LoginComponent implements OnInit
{
    loginAttempt: LoginRequestUser
    isAuthenticated$!: Observable<boolean>
    error$!: Observable<ErrorValue[] | null>
    containerHeight: number

    constructor( private readonly store: Store<AuthState.State> )
    {
        this.loginAttempt = { username: '', password: '', remember_me: false }
        this.containerHeight = fixedHeight
    }

    ngOnInit(): void
    {
        this.isAuthenticated$ = this.store.select( AuthSelectors.selectIsAuthenticated )
        this.error$ = this.store.select( AuthSelectors.selectError )
    }

    @HostListener( 'window:resize', [ '$event' ] )
    onResize(): void
    {
        this.containerHeight = fixedHeight
    }

    login( loginAttempt: LoginRequestUser ): void
    {
        this.store.dispatch( AuthActions.loginRequest( { loginRequestUser: loginAttempt } ) )
    }

    isValid( loginAttemptUser: LoginRequestUser ): boolean
    {
        // TODO enforce email regex check
        return !!( loginAttemptUser.username && loginAttemptUser.password )
    }
}
