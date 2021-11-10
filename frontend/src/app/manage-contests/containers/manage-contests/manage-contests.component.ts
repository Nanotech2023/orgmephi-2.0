import { Component, OnInit, ViewChild } from '@angular/core'
import { TasksService } from '@api/tasks/tasks.service'
import { CompositeContest, SimpleContest } from '@api/tasks/model'
import { DxDataGridComponent } from 'devextreme-angular'
import { ActivatedRoute, Router } from '@angular/router'
import CompositeTypeEnum = SimpleContest.CompositeTypeEnum


@Component( {
    selector: 'app-manage-contests',
    templateUrl: './manage-contests.component.html',
    styleUrls: [ './manage-contests.component.scss' ]
} )
export class ManageContestsComponent implements OnInit
{
    constructor( private route: ActivatedRoute, private router: Router, private tasksService: TasksService ) { }

    ngOnInit(): void
    {
        this.tasksService.tasksUnauthorizedOlympiadAllGet( undefined, undefined, undefined, undefined, undefined, undefined, undefined, undefined, CompositeTypeEnum.SimpleContest ).subscribe( response =>
        {
            this.simpleContests = response.contest_list! as SimpleContest[]
        } )
    }

    simpleContestId!: number
    simpleContests!: SimpleContest[]

    @ViewChild( DxDataGridComponent, { static: false } ) grid!: DxDataGridComponent
    selectedRowIndex: number = -1
    selectedRow?: SimpleContest = undefined
    previousParticipationConditionEnum: ( "Winner 1" | "Winner 2" | "Winner 3" | "Diploma 1" | "Diploma 2" | "Diploma 3" | "Participant" )[] = Object.values( SimpleContest.PreviousParticipationConditionEnum )
    holdingTypeEnum: ( "OfflineContest" | "OnLineContest" )[] = Object.values( SimpleContest.HoldingTypeEnum )
    statusEnum: ( "Will start soon" | "In progress" | "Finished" )[] = Object.values( SimpleContest.StatusEnum )

    navigateElement(): void
    {
        if ( this.selectedRow )
        {
            const routePath = [ '/manage', 'contests', this.selectedRow.base_contest.base_contest_id, 'contest', this.selectedRow.contest_id, 'users' ]
            this.router.navigate( routePath )
        }
    }

    navigateElement2(): void
    {
        if ( this.selectedRow )
        {
            const routePath = [ '/manage', 'contests', this.selectedRow.base_contest.base_contest_id, 'contest', this.selectedRow.contest_id, 'variants' ]
            this.router.navigate( routePath )
        }
    }

    editElement(): void
    {
        this.grid.instance.editRow( this.selectedRowIndex )
        this.grid.instance.deselectAll()
    }

    deleteElement(): void
    {
        this.grid.instance.deleteRow( this.selectedRowIndex )
        this.grid.instance.deselectAll()
    }

    addElement(): void
    {
        this.grid.instance.addRow()
        this.grid.instance.deselectAll()
    }

    selectedChanged( $event: any ): void
    {
        this.selectedRow = $event.selectedRowsData[ 0 ]
        this.selectedRowIndex = $event.component.getRowIndexByKey( $event.selectedRowKeys[ 0 ] )
    }
}
