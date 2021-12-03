import { Component } from '@angular/core'
import { ContestsStore } from '@/contests/contests.store'
import { OlympiadLocation, SimpleContest } from '@api/tasks/model'
import { Observable } from 'rxjs'
import { TasksService } from '@api/tasks/tasks.service'
import { ActivatedRoute, Router } from '@angular/router'
import { ResponsesService } from '@api/responses/responses.service'
import { UserResponseStatusResponse } from '@api/responses/model'


@Component( {
    selector: 'app-contest-registration',
    templateUrl: './contest-registration.component.html',
    styleUrls: [ './contest-registration.component.scss' ]
} )
export class ContestRegistrationComponent
{
    contest$: Observable<SimpleContest | undefined>
    locations!: Array<OlympiadLocation>
    contestId!: number | null
    contestStatus$!: Observable<UserResponseStatusResponse>

    constructor( private route: ActivatedRoute, private contestsStore: ContestsStore, private tasksService: TasksService, private responsesService: ResponsesService, private router: Router )
    {
        this.route.paramMap.subscribe( paramMap =>
        {
            this.contestId = Number( paramMap.get( 'contestId' ) )
            if ( !!this.contestId )
            {
                this.contestsStore.fetchSingle( this.contestId )
                this.contestStatus$ = this.responsesService.responsesParticipantContestContestIdUserSelfStatusGet( this.contestId )
            }
        } )
        this.contest$ = this.contestsStore.contest$
        this.tasksService.tasksUnauthorizedLocationAllGet().subscribe( items => this.locations = items.locations )
    }

    onStartClick( contestId: number | undefined ): void
    {
        // TODO allow select other locations
        const locationId = 3
        const contestIdNumber = contestId as number
        this.contestsStore.enroll( {
            contestId: contestIdNumber,
            locationId: locationId
        } )
        this.contestsStore.start( contestIdNumber )
        this.router.navigate( [ `/contests/${ contestId }/assignment` ] )
    }

    inProgress( contestStatus: UserResponseStatusResponse ): boolean
    {
        return contestStatus.status === UserResponseStatusResponse.StatusEnum.InProgress
    }

    finished( contestStatus: UserResponseStatusResponse ): boolean
    {
        return !this.inProgress( contestStatus )
    }
}
