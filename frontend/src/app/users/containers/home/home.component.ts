import { Component, OnInit } from '@angular/core'
import { select, Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'
import { Observable } from 'rxjs'
import { TypeUserInfo } from '@/auth/api/models'


@Component( {
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: [ './home.component.scss' ]
} )
export class HomeComponent implements OnInit
{
    user$!: Observable<TypeUserInfo | null>

    constructor( private store: Store<AuthState.State> ) {}

    ngOnInit(): void
    {
        this.user$ = this.store.pipe( select( AuthSelectors.selectUserInfo ) )
    }

    isStudent( userInfo: TypeUserInfo | null )
    {
        return userInfo?.role == 'Participant'
    }
}
