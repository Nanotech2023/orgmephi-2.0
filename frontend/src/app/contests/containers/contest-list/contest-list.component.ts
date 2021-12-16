import { Component, OnDestroy, OnInit } from '@angular/core'
import { select, Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'
import { Observable, Subscription } from 'rxjs'
import { Contest, SimpleContestWithFlagResponseTaskParticipant } from '@api/tasks/model'
import { ContestsStore } from '@/contests/contests.store'
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router'
import { filter, startWith } from 'rxjs/operators'


@Component( {
    selector: 'app-contest-list',
    templateUrl: './contest-list.component.html',
    styleUrls: [ './contest-list.component.scss' ]
} )
export class ContestListComponent implements OnInit, OnDestroy
{
    isParticipant$!: Observable<boolean>

    showContestsList: boolean
    contests$: Observable<SimpleContestWithFlagResponseTaskParticipant[]>
    urlSubscription!: Subscription

    constructor( private authStore: Store<AuthState.State>, private contestsStore: ContestsStore, private router: Router )
    {
        this.showContestsList = false
        this.contests$ = this.contestsStore.contests$
    }

    ngOnInit(): void
    {
        this.isParticipant$ = this.authStore.pipe( select( AuthSelectors.selectIsParticipant ) )
        this.urlSubscription = this.router.events.pipe(
            filter( ( event ) => event instanceof NavigationEnd ),
            startWith( this.router )
        ).subscribe( ( event ) =>
        {
            console.log( 'enter ContestListComponent/urlSubscription' )
            this.contestsStore.fetchSchoolInfo()
            this.contestsStore.fetchAll()
        } )
    }

    ngOnDestroy(): void
    {
        this.urlSubscription?.unsubscribe()
    }

    collapseContestsList(): void
    {
        this.showContestsList = !this.showContestsList
    }

    getTargetClassesDisplay( contest: Contest ): string
    {
        return contest.base_contest?.target_classes?.map( item => item.target_class ).join( "," ) + " классы"
    }

}
