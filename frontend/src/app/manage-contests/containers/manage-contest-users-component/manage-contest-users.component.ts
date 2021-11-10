import { Component, ViewChild } from '@angular/core'
import { UserInContest } from '@api/tasks/model'
import { DxDataGridComponent } from 'devextreme-angular'
import { ActivatedRoute, Router } from '@angular/router'
import { TasksService } from '@api/tasks/tasks.service'


@Component( {
    selector: 'app-manage-contest-users',
    templateUrl: './manage-contest-users.component.html',
    styleUrls: [ './manage-contest-users.component.scss' ]
} )
export class ManageContestUsersComponent
{
    constructor( private route: ActivatedRoute, private router: Router, private tasksService: TasksService )
    {
        this.route.paramMap.subscribe( paramMap =>
        {
            this.simpleContestId = Number( paramMap.get( 'simpleContestId' ) )
            if ( !!this.simpleContestId )
            {
                this.tasksService.tasksControlUsersContestIdContestUserAllGet( this.simpleContestId ).subscribe( response =>
                {
                    this.users = response.user_list
                } )
            }
        } )
    }

    simpleContestId!: number
    users: Array<UserInContest> = []

    @ViewChild( DxDataGridComponent, { static: false } ) grid!: DxDataGridComponent
    selectedRowIndex: number = -1
    selectedRow?: UserInContest = undefined
    userStatusEnum: ( "Winner 1" | "Winner 2" | "Winner 3" | "Diploma 1" | "Diploma 2" | "Diploma 3" | "Participant" )[] = Object.values( UserInContest.UserStatusEnum )

    navigateElement(): void
    {
        if ( this.selectedRow )
            this.router.navigate( [ this.selectedRow.user_id, 'assignment' ], { relativeTo: this.route } )
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