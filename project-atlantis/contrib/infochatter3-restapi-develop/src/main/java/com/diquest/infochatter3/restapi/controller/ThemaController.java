package com.diquest.infochatter3.restapi.controller;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import com.diquest.infochatter3.client.Infochatter3Client;
import com.diquest.infochatter3.client.module.thema.entity.ThemaRequest;
import com.diquest.infochatter3.client.module.thema.entity.ThemaResponse;
import com.diquest.infochatter3.client.module.thema.entity.ThemaResponse.Thema;
import com.diquest.infochatter3.restapi.model.ThemaRequest.Auth;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;

@Slf4j
@Api(description = "테마")
@RequestMapping(value = {"/thema"}, method = {RequestMethod.POST}, consumes = {"application/json"},
    produces = {"application/json"})
@RestController
public class ThemaController {

  @Autowired
  private Infochatter3Client client;

  @ApiOperation("테마정보")
  @RequestMapping({"/thema"})
  public Thema thema(@RequestBody Auth request) throws Exception {
    ThemaRequest in = new ThemaRequest();
    in.setAgentName(request.getAgentName());
    in.setRepoId(request.getRepoId());
    ThemaResponse out = client.thema().getThema(in);

    if (out == null) {
      return null;
    }

    Thema thema = out.getThema();

    if (thema.getDeployId() == null || !thema.getDeployId().equals(request.getDeployId())) {
      return null;
    }

    return thema;
  }

  @ApiOperation("테마정보 2")
  @RequestMapping({"/info"})
  public Thema info(@RequestBody Auth request) throws Exception {
    ThemaRequest in = new ThemaRequest();
    log.info("theme info / agent:[{}], repo:[{}], deploy:[{}]", request.getAgentName(), request.getRepoId(), request.getDeployId());
    in.setAgentName(request.getAgentName());
    in.setRepoId(request.getRepoId());
    ThemaResponse out = client.thema().getThema(in);

    if (out == null) {
      return null;
    }

    Thema thema = out.getThema();

    if (thema.getDeployId() == null || !thema.getDeployId().equals(request.getDeployId())) {
      return null;
    }

    return thema;
  }
}
