import { Component, OnInit, ViewChild } from '@angular/core'
import { ActivatedRoute, Router } from '@angular/router'
import { UserInContest } from '@api/tasks/model'
import { DxDataGridComponent } from 'devextreme-angular'
import { ResponsesService } from '@api/responses/responses.service'
import {
    AllUserAnswersResponse,
    AllUserMarksResponse,
    UserResponseStatusResponse,
    UserTimeResponseRequest
} from '@api/responses/model'
import { Observable } from 'rxjs'
import { ManageContestUserAssignmentStore } from '@/manage-contests/containers/manage-contest-user-assignment/manage-contest-user-assignment.store'


@Component( {
    selector: 'app-manage-contest-user-assignment',
    templateUrl: './manage-contest-user-assignment.component.html',
    styleUrls: [ './manage-contest-user-assignment.component.scss' ],
    providers: [ ManageContestUserAssignmentStore ]
} )
export class ManageContestUserAssignmentComponent implements OnInit
{
    viewModel$: Observable<{
        userResponse: AllUserAnswersResponse,
        userStatus: UserResponseStatusResponse,
        userMark: AllUserMarksResponse,
        userTime: UserTimeResponseRequest,
        userExtraTime: UserTimeResponseRequest,
    }> = this.store.viewModel$

    constructor( private store: ManageContestUserAssignmentStore, private route: ActivatedRoute ) { }


    ngOnInit(): void
    {
        this.route.paramMap.subscribe( paramMap =>
        {
            this.simpleContestId = Number( paramMap.get( 'simpleContestId' ) )
            this.userId = Number( paramMap.get( 'userId' ) )
            if ( !!this.simpleContestId && !!this.userId )
            {
                const contestUserAssignment: { contestId: number, userId: number } = {
                    contestId: this.simpleContestId,
                    userId: this.userId
                }
                this.store.fetchUserResponse( contestUserAssignment )
                this.store.fetchUserStatus( contestUserAssignment )
                this.store.fetchUserMark( contestUserAssignment )
                this.store.fetchUserTime( contestUserAssignment )
                this.store.fetchUserExtraTime( contestUserAssignment )
            }
        } )
    }

    simpleContestId!: number
    userId!: number

    userResponse$!: Observable<AllUserAnswersResponse>
    userStatus$!: Observable<UserResponseStatusResponse>
    userMark$!: Observable<AllUserMarksResponse>
    userTime$!: Observable<UserTimeResponseRequest>
    userExtraTime$!: Observable<UserTimeResponseRequest>

    @ViewChild( DxDataGridComponent, { static: false } ) grid!: DxDataGridComponent
    selectedRowIndex: number = -1
    selectedRow?: UserInContest = undefined

    addElement(): void
    {
        this.grid.instance.addRow()
        this.grid.instance.deselectAll()
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

    selectedChanged( $event: any ): void
    {
        this.selectedRow = $event.selectedRowsData[ 0 ]
        this.selectedRowIndex = $event.component.getRowIndexByKey( $event.selectedRowKeys[ 0 ] )
    }

}
