import { Component, HostListener, OnInit } from '@angular/core'
import { Store } from '@ngrx/store'
import { AuthActions, AuthSelectors, AuthState } from '@/auth/store'
import { Observable } from 'rxjs'
import { AuthCredentials } from '@/auth/models'
import { fixedHeight } from '@/shared/consts'


@Component( {
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: [ './login.component.scss' ]
} )
export class LoginComponent implements OnInit
{
    loginAttempt: AuthCredentials
    isAuthenticated$!: Observable<boolean>
    error$!: Observable<string | null>
    containerHeight: number

    constructor( private readonly store: Store<AuthState.State> )
    {
        this.loginAttempt = { username: '', password: '' }
        this.containerHeight = fixedHeight
    }

    ngOnInit(): void
    {
        this.isAuthenticated$ = this.store.select( AuthSelectors.selectIsAuthenticated )
        this.error$ = this.store.select( AuthSelectors.selectError )
    }

    @HostListener( 'window:resize', [ '$event' ] )
    onResize()
    {
        this.containerHeight = fixedHeight
    }

    login( loginAttemptUser: AuthCredentials ): void
    {
        const authentication = { authentication: { authCredentials: loginAttemptUser } }
        this.store.dispatch( AuthActions.loginAttempt( authentication ) )
    }

    isValid( loginAttemptUser: AuthCredentials ): boolean
    {
        // TODO enforce email regex check
        return !!( loginAttemptUser.password && loginAttemptUser.username )
    }
}
