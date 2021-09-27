import { Component } from '@angular/core'
import { ContestsStore } from '@/contests/contests.store'
import {
    AllLocationResponseTaskUnauthorized,
    OlympiadLocation,
    SimpleContestWithFlagResponseTaskParticipant
} from '@api/tasks/model'
import { Observable } from 'rxjs'
import { TasksService } from '@api/tasks/tasks.service'


@Component( {
    selector: 'app-contest-registration',
    templateUrl: './contest-registration.component.html',
    styleUrls: [ './contest-registration.component.scss' ]
} )
export class ContestRegistrationComponent
{
    contest$: Observable<SimpleContestWithFlagResponseTaskParticipant | undefined>
    locations!: Array<OlympiadLocation>

    constructor( private contestsStore: ContestsStore, private tasksService: TasksService )
    {
        this.contest$ = contestsStore.selectedContest
        this.tasksService.tasksUnauthorizedLocationAllGet().subscribe( items => this.locations = items.locations )
    }

    onEnrollClick( contestId: number | undefined )
    {
        // TODO allow select other locations
        const locationId = 2
        if ( contestId as number )
        {
            this.contestsStore.enroll( {
                contestId: contestId as number,
                enrollRequestTaskParticipant: { location_id: locationId }
            } )
        }
    }

    onStartClick( contestId: number | undefined ): void
    {
        if ( contestId as number )
        {
            this.contestsStore.getVariant( contestId as number )
        }
    }
}
