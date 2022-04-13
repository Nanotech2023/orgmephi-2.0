import { Component, OnInit, ViewChild } from '@angular/core'
import { ContestResultsStore } from '@/contests/containers/contest-results/contest-results.store'
import { Observable } from 'rxjs'
import { ContestInfo, UserResultsForContestResponse } from '@api/responses/model'
import { AgGridAngular } from 'ag-grid-angular'
import { ResponsesService } from '@api/responses/responses.service'
import { TasksService } from '@api/tasks/tasks.service'


@Component( {
    selector: 'app-contest-results',
    templateUrl: './contest-results.component.html',
    styleUrls: [ './contest-results.component.scss' ],
    providers: [ ContestResultsStore ]
} )
export class ContestResultsComponent implements OnInit
{
    results$: Observable<UserResultsForContestResponse[]>
    public overlayNoRowsTemplate = 'Дипломы для скачивания отсутствуют или не сформированы'
    columnDefs = [
        { headerName: "ID", field: "contest_info.contest_id", width: 1, hide: true, suppressToolPanel: true },
        {
            field: 'contest_info.name',
            sortable: true,
            filter: true,
            headerName: 'Мероприятие',
            autoHeight: true,
            wrapText: true,
            width: 500
        },
        { field: 'contest_info.start_year', sortable: true, filter: true, headerName: 'Год' },
        { field: 'contest_info.subject', sortable: true, filter: true, headerName: 'Предмет' },
        { field: 'mark', headerName: 'Балл' },
        { field: 'user_status', headerName: 'Димпломы' },
        { field: 'status', sortable: true, filter: true, headerName: 'Статус' }
    ]
    @ViewChild( 'table_contest_results' ) agGrid!: AgGridAngular

    constructor( private contestResultsStore: ContestResultsStore, private tasksService: TasksService )
    {
        this.results$ = contestResultsStore.results$
    }

    ngOnInit(): void
    {
        this.contestResultsStore.fetchAll()
    }

    getRowNodeId( data: UserResultsForContestResponse ): number | undefined
    {
        return data.contest_info.contest_id
    }

    download()
    {
        const selectedRows = this.agGrid.api.getSelectedRows()
        if ( selectedRows.length !== 0 )
        {
            const selectedContest: UserResultsForContestResponse = selectedRows[ 0 ]
            this.tasksService.tasksParticipantContestIdContestCertificateSelfGet( selectedContest.contest_info.contest_id ).subscribe( item => this.downloadFile( item ) )
        }
    }

    downloadFile( data: Blob )
    {
        const blob = new Blob( [ data ], { type: 'application/pdf' } )
        const url = window.URL.createObjectURL( blob )
        window.open( url )
    }
}
