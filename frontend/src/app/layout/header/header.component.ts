import { Component } from '@angular/core'
import { select, Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'
import { Observable } from 'rxjs'
import { UserInfo } from '@api/users/models'


@Component( {
    selector: 'app-header',
    templateUrl: './header.component.html',
    styleUrls: [ './header.component.scss' ]
} )
export class HeaderComponent
{
    personalInfo$: Observable<UserInfo>

    constructor( private authStore: Store<AuthState.State> )
    {
        this.personalInfo$ = this.authStore.pipe( select( AuthSelectors.selectUserInfo ) )
    }
}