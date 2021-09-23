import { Component } from '@angular/core'
import { Observable } from 'rxjs'
import { ContestsStore } from '@/contests/contests.store'
import { Contest } from '@api/tasks/model'


@Component( {
    selector: 'app-contest-details',
    templateUrl: './contest-details.component.html',
    styleUrls: [ './contest-details.component.scss' ]
} )
export class ContestDetailsComponent
{
    contest$: Observable<Contest | undefined>

    constructor( private contestsStore: ContestsStore )
    {
        this.contest$ = this.contestsStore.selectedContest
    }

    onEnrollClick( contestId: number, locationId: number )
    {
        this.contestsStore.enroll( {
            contestId: contestId,
            enrollRequestTaskParticipant: { location_id: locationId }
        } )
    }

    onStartClick( contestId: number ): void
    {
        this.contestsStore.getVariant( contestId )
    }

    getTargetClassesDisplay( contest: Contest ): string
    {
        return contest.base_contest?.target_classes?.map( item => item.target_class ).join( "," ) + " классы"
    }
}