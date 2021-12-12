import { Component, OnInit } from '@angular/core'
import { Observable } from 'rxjs'
import { UserInfo } from '@api/users/models'
import { select, Store } from '@ngrx/store'
import { AuthActions, AuthSelectors, AuthState } from '@/auth/store'


@Component( {
    selector: 'app-header-menu',
    templateUrl: './header-menu.component.html',
    styleUrls: [ './header-menu.component.scss' ]
} )
export class HeaderMenuComponent implements OnInit
{
    personalInfo$!: Observable<UserInfo>
    isPrivileged$!: Observable<boolean>

    constructor( private store: Store<AuthState.State> )
    {
    }

    ngOnInit(): void
    {
        this.personalInfo$ = this.store.pipe( select( AuthSelectors.selectUserInfo ) )
        this.isPrivileged$ = this.store.select( AuthSelectors.selectIsPrivileged )
    }

    logoutButtonClick(): void
    {
        this.store.dispatch( AuthActions.logoutRequest() )
    }
}
