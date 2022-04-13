import { Component, OnDestroy, OnInit } from '@angular/core'
import { select, Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'
import { Observable, Subscription } from 'rxjs'
import { Contest, SimpleContestWithFlagResponseTaskParticipant } from '@api/tasks/model'
import { ContestListStore } from '@/contests/containers/contest-list/contest-list.store'
import { Router } from '@angular/router'
import { UsersService } from '@api/users/users.service'
import { SchoolInfo } from '@api/users/models'


@Component( {
    selector: 'app-contest-list',
    templateUrl: './contest-list.component.html',
    styleUrls: [ './contest-list.component.scss' ],
    providers: [ ContestListStore ]
} )
export class ContestListComponent implements OnInit, OnDestroy
{
    isParticipant$!: Observable<boolean>

    showContestsList: boolean
    contests$: Observable<SimpleContestWithFlagResponseTaskParticipant[]>
    urlSubscription!: Subscription

    constructor( private authStore: Store<AuthState.State>, private contestListStore: ContestListStore, private router: Router, private usersService: UsersService )
    {
        this.showContestsList = false
        this.contests$ = this.contestListStore.contests$
    }

    ngOnInit(): void
    {
        this.isParticipant$ = this.authStore.pipe( select( AuthSelectors.selectIsParticipant ) )
        this.usersService.userProfileSchoolGet().subscribe( ( response: SchoolInfo ) => this.contestListStore.fetchAll( response!.grade! ) )
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
