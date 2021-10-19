import { Component } from '@angular/core'
import { Observable } from 'rxjs'
import { UserInfo } from '@api/users/models'
import { select, Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'


@Component( {
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: [ './home.component.scss' ]
} )
export class HomeComponent
{
    personalInfo$: Observable<UserInfo>

    constructor( private authStore: Store<AuthState.State> )
    {
        this.personalInfo$ = this.authStore.pipe( select( AuthSelectors.selectUserInfo ) )
    }
}
