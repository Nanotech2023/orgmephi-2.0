import { Component, OnInit } from '@angular/core'
import { select, Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'
import { Observable } from 'rxjs'
import { fixedHeight } from '@/shared/consts'


@Component( {
    selector: 'app-root',
    templateUrl: './app.component.html'
} )
export class AppComponent implements OnInit
{
    isAuthorized$!: Observable<boolean>

    constructor( private store: Store<AuthState.State> ) {}

    title = 'MEPhI-Olymp'

    ngOnInit(): void
    {
        this.isAuthorized$ = this.store.pipe( select( AuthSelectors.selectIsAuthenticated ) )
    }
}