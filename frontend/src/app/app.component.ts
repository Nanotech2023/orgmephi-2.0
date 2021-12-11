import { Component, OnDestroy, OnInit } from '@angular/core'
import { select, Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'
import { Observable, SubscriptionLike } from 'rxjs'
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router'
import { filter, startWith } from 'rxjs/operators'


@Component( {
    selector: 'app-root',
    templateUrl: './app.component.html'
} )
export class AppComponent implements OnInit, OnDestroy
{
    isAuthorized$!: Observable<boolean>
    urlSubscription: SubscriptionLike
    showHeader: boolean | undefined
    selectIsConfirmed$!: Observable<boolean>

    constructor( private store: Store<AuthState.State>, private router: Router )
    {
        this.urlSubscription = this.router.events.pipe(
            filter( ( event ) => event instanceof NavigationEnd ),
            startWith( this.router )
        ).subscribe( ( event ) =>
        {
            if ( event instanceof NavigationEnd )
                this.showHeader = event.url != "/login"
        } )
    }

    title = 'ORG MEPhI'

    ngOnInit(): void
    {
        this.isAuthorized$ = this.store.pipe( select( AuthSelectors.selectIsAuthorized ) )
        this.selectIsConfirmed$ = this.store.pipe( select( AuthSelectors.selectIsConfirmed ) )
    }

    ngOnDestroy(): void
    {
        this.urlSubscription?.unsubscribe()
    }
}