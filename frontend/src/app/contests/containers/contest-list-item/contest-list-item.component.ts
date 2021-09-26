import { Component, Input } from '@angular/core'
import { Contest } from '@api/tasks/model'
import { Router } from '@angular/router'
import { ContestsStore } from '@/contests/contests.store'


@Component( {
    selector: 'app-contest-list-item',
    templateUrl: './contest-list-item.component.html',
    styleUrls: [ './contest-list-item.component.scss' ]
} )
export class ContestListItemComponent
{
    // @ts-ignore
    @Input() contest: Contest

    constructor( private contestsStore: ContestsStore, private router: Router )
    {
    }

    navigateTo(): Promise<boolean>
    {
        this.contestsStore.selectContest( this.contest )
        return this.router.navigate( [ "/contests", this.contest.contest_id ] )
    }
}
